package daikon.inv.unary.sequence;

import daikon.PptSlice;
import daikon.inv.Invariant;
import daikon.inv.InvariantStatus;
import daikon.inv.OutputFormat;
import typequals.prototype.qual.NonPrototype;
import java.util.logging.Logger;

import daikon.Global;
import daikon.VarInfo;
import daikon.inv.ValueSet;
import typequals.prototype.qual.Prototype;
import org.plumelib.util.Intern;

import org.checkerframework.checker.interning.qual.Interned;
import org.checkerframework.checker.lock.qual.GuardSatisfied;
import org.checkerframework.checker.nullness.qual.Nullable;
import org.checkerframework.dataflow.qual.Pure;
import org.checkerframework.dataflow.qual.SideEffectFree;

public class InvConBalanceSum1 extends SingleFloatSequence {
    // We are Serializable, so we specify a version to allow changes to
    // method signatures without breaking serialization.  If you add or
    // remove fields, you should change this number to the current date.
    static final long serialVersionUID = 20211003L;

    // Variables starting with dkconfig_ should only be set via the
    // daikon.config.Configuration interface.
    /** Boolean. True iff SeqFloatEqual invariants should be considered. */
    public static boolean dkconfig_enabled = Invariant.invariantEnabledDefault;

    public static final Logger debug =
        Logger.getLogger("daikon.inv.binary.sequenceScalar.InvConBalanceSum1");

    static boolean debugSeqIntComparison = false;

    public double BookSum = Double.MAX_VALUE;

    InvConBalanceSum1(PptSlice ppt) {
        super(ppt);
    }

    @Prototype InvConBalanceSum1() {
        super();
    }

    private static @Prototype InvConBalanceSum1 proto = new @Prototype InvConBalanceSum1();

    /** Returns the prototype invariant for SeqFloatEqual */
    public static @Prototype InvConBalanceSum1 get_proto() {
        return proto;
    }

    /** Returns whether or not this invariant is enabled. */
    @Override
    public boolean enabled() {
        return dkconfig_enabled;
    }

    @Override
    public InvariantStatus add_modified(double @Interned [] value, int count) {
        // TODO Auto-generated method stub
        return check_modified(value, count);
    }

    @Override
    public InvariantStatus check_modified(double @Interned [] value, int count) {
        // TODO Auto-generated method stub
        double sum=0;
        for (int i = 0; i < value.length; i++) {
            sum += value[i];
        }
        // assert seqvar().type.elementIsIntegral();
        if (Global.fuzzy.eq(BookSum, Double.MAX_VALUE)){
            BookSum = sum;
        }else 
            if (!Global.fuzzy.eq(sum, BookSum)) {
                    return InvariantStatus.FALSIFIED;
            }
        return InvariantStatus.NO_CHANGE;
    }

    @Override
    protected double computeConfidence() {
        if (Global.fuzzy.eq(BookSum, Double.MAX_VALUE)){
            return 0;
        }

        // TODO Auto-generated method stub
        if (ppt.num_samples() == 0) {
            return CONFIDENCE_UNJUSTIFIED;
        }
      
        // If the array never has any elements, its unjustified
        ValueSet.ValueSetFloatArray vs = (ValueSet.ValueSetFloatArray) var().get_value_set();
        if (vs.elem_cnt() == 0) {
            return CONFIDENCE_UNJUSTIFIED;
        } 
        // return 1 - Math.pow(.5, vs.elem_cnt());
        return 1 - Math.pow(.5, ppt.num_samples());
    }

    @Override
    public String format_using(OutputFormat format) {
        
    if (format.isJavaFamily()) {
        return format_java_family(format);
      }
  
      if (format == OutputFormat.DAIKON) {
        return format_daikon();
      }
      if (format == OutputFormat.ESCJAVA) {
        return format_esc();
      }
      if (format == OutputFormat.SIMPLIFY) {
        return format_simplify();
      }
      if (format == OutputFormat.CSHARPCONTRACT) {
        return format_csharp_contract();
      }
  
      return format_unimplemented(format);
    }

    private String format_csharp_contract() {
        String[] split = var().csharp_array_split();
        return "Contract.ForalleltsSUM1("
        + split[0]
        + ", x => x"
        + split[1]
        + " == "
        + BookSum
        + ")";
    }

    private String format_simplify() {
        String[] form = VarInfo.simplify_quantify(var());
        return form[0] + "(SUMEQ1 " + form[1] + " " + BookSum + ")" + form[2];
    }

    private String format_esc() {
        String[] form = VarInfo.esc_quantify(var());
        return form[0] + "( SUM1(" + form[1] + ") == " + BookSum + ")" + form[2];
    }

    private String format_daikon() {
        return var().name() + " SUM1 (elements) == " + BookSum;
    }

    private String format_java_family(OutputFormat format) {
        return "daikon.Quant.eltsSUMEqual("
        + var().name_using(format)
        + ", "
        + BookSum
        + ")";
    }

    @Override
    public boolean isSameFormula(Invariant other) {
        // TODO Auto-generated method stub
        return true;
    }

    @Override
    protected @NonPrototype Invariant instantiate_dyn(PptSlice slice) {
        // TODO Auto-generated method stub
        return new InvConBalanceSum1(slice);
    }

}
