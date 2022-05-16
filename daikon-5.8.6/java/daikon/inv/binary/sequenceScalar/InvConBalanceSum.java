package daikon.inv.binary.sequenceScalar;

import java.util.logging.Logger;

import daikon.Global;
import daikon.PptSlice;
import daikon.VarInfo;
import daikon.inv.Invariant;
import daikon.inv.InvariantStatus;
import daikon.inv.OutputFormat;
import daikon.inv.ValueSet;
import typequals.prototype.qual.NonPrototype;
import typequals.prototype.qual.Prototype;
import org.plumelib.util.Intern;

import org.checkerframework.checker.interning.qual.Interned;
import org.checkerframework.checker.lock.qual.GuardSatisfied;
import org.checkerframework.checker.nullness.qual.Nullable;
import org.checkerframework.dataflow.qual.Pure;
import org.checkerframework.dataflow.qual.SideEffectFree;

public class InvConBalanceSum extends SequenceFloat{
    // We are Serializable, so we specify a version to allow changes to
    // method signatures without breaking serialization.  If you add or
    // remove fields, you should change this number to the current date.
    static final long serialVersionUID = 20211003L;

    // Variables starting with dkconfig_ should only be set via the
    // daikon.config.Configuration interface.
    /** Boolean. True iff SeqFloatEqual invariants should be considered. */
    public static boolean dkconfig_enabled = Invariant.invariantEnabledDefault;

    public static final Logger debug =
        Logger.getLogger("daikon.inv.binary.sequenceScalar.InvConBalanceSum");

    static boolean debugSeqIntComparison = false;

    InvConBalanceSum(PptSlice ppt) {
        super(ppt);
    }

    @Prototype InvConBalanceSum() {
        super();
    }

    private static @Prototype InvConBalanceSum proto = new @Prototype InvConBalanceSum();

    /** Returns the prototype invariant for SeqFloatEqual */
    public static @Prototype InvConBalanceSum get_proto() {
        return proto;
    }

    /** Returns whether or not this invariant is enabled. */
    @Override
    public boolean enabled() {
        return dkconfig_enabled;
    }

    @Override
    public InvariantStatus check_modified(double @Interned [] v1, double v2, int count) {
        // TODO Auto-generated method stub
         /*if (logDetail() || debug.isLoggable(Level.FINE))
        log(debug,"(<= " + Arrays.toString(a)
        + " " + x);*/
        double sum=0;
        for (int i = 0; i < v1.length; i++) {
            sum += v1[i];
        }
        // assert seqvar().type.elementIsIntegral();

        if (!Global.fuzzy.eq(sum, v2)) {
                return InvariantStatus.FALSIFIED;
        }
        
        return InvariantStatus.NO_CHANGE;
    }

    @Override
    public InvariantStatus add_modified(double @Interned [] v1, double v2, int count) {
        // TODO Auto-generated method stub
        return check_modified(v1, v2, count);
    }

    @Override
    protected double computeConfidence() {
        // TODO Auto-generated method stub
       
        if (ppt.num_samples() == 0) {
          return CONFIDENCE_UNJUSTIFIED;
        }
    
        // If the array never has any elements, its unjustified
        ValueSet.ValueSetFloatArray vs = (ValueSet.ValueSetFloatArray) seqvar().get_value_set();
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
        String[] split = seqvar().csharp_array_split();
        return "Contract.ForalleltsSUM("
        + split[0]
        + ", x => x"
        + split[1]
        + " == "
        + sclvar().csharp_name()
        + ")";
    }

    private String format_simplify() {
        String[] form = VarInfo.simplify_quantify(seqvar(), sclvar());
        return form[0] + "(SUMEQ " + form[1] + " " + form[2] + ")" + form[3];
    }

    private String format_esc() {
        String[] form = VarInfo.esc_quantify(seqvar(), sclvar());
        return form[0] + "( SUM(" + form[1] + ") == " + form[2] + ")" + form[3];
    }

    private String format_daikon() {
        return seqvar().name() + " SUM (elements) == " + sclvar().name();
    }

    private String format_java_family(OutputFormat format) {
        return "daikon.Quant.eltsSUMEqual("
        + seqvar().name_using(format)
        + ", "
        + sclvar().name_using(format)
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
        return new InvConBalanceSum(slice);
    }
}
