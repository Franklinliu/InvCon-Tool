package daikon.derive.ternary;

import daikon.ValueTuple;
import daikon.VarInfo;
import daikon.derive.Derivation;
import daikon.derive.ValueAndModified;
import org.plumelib.util.ArraysPlume;
import org.plumelib.util.Intern;

import org.checkerframework.dataflow.qual.SideEffectFree;
import org.checkerframework.dataflow.qual.Pure;
import org.checkerframework.checker.interning.qual.Interned;

import java.math.BigInteger;
public final class InvConUserBookkeeping extends TernaryDerivation {
    // We are Serializable, so we specify a version to allow changes to
    // method signatures without breaking serialization.  If you add or
    // remove fields, you should change this number to the current date.
    static final long serialVersionUID = 20101004L;

    // Variables starting with dkconfig_ should only be set via the
    // daikon.config.Configuration interface.
    /** Boolean. True iff InvConUserBalance derived variables should be generated. */
    public static boolean dkconfig_enabled = false;

    protected InvConUserBookkeeping(VarInfo vi1, VarInfo vi2, VarInfo vi3) {
        super(vi1, vi2, vi3);
        //TODO Auto-generated constructor stub
    }

    public VarInfo enclose_keys_var() {
        return base1;
    }

    public VarInfo values_var() {
        return base2;
    }

    public VarInfo key_var() {
        return base3;
    }

    @Override
    public ValueAndModified computeValueAndModified(ValueTuple full_vt) {
        // TODO Auto-generated method stub
        int mod1 = base1.getModified(full_vt);
        if (mod1 == ValueTuple.MISSING_NONSENSICAL) {
          return ValueAndModified.MISSING_NONSENSICAL;
        }
        int mod2 = base2.getModified(full_vt);
        if (mod2 == ValueTuple.MISSING_NONSENSICAL) {
          return ValueAndModified.MISSING_NONSENSICAL;
        }
        int mod3 = base3.getModified(full_vt);
        if (mod3 == ValueTuple.MISSING_NONSENSICAL) {
          return ValueAndModified.MISSING_NONSENSICAL;
        }

        Object val1 =  base1.getValue(full_vt);
        if (val1 == null) {
            return ValueAndModified.MISSING_NONSENSICAL;
        }

        Object val2 =  base2.getValue(full_vt);
        if (val2 == null) {
            return ValueAndModified.MISSING_NONSENSICAL;
        }
        Object val3 = base3.getValue(full_vt);
        if (val3 == null) {
            return ValueAndModified.MISSING_NONSENSICAL;
        }

        int mod =
            (((mod1 == ValueTuple.UNMODIFIED)
            && (mod2 == ValueTuple.UNMODIFIED)
            && (mod3 == ValueTuple.UNMODIFIED))
            ? ValueTuple.UNMODIFIED
            : ValueTuple.MODIFIED);
        
        int val1_size = 0;
        int val2_size = 0;
        if (val1 instanceof String[]){
            val1_size = ((String[])val1).length;
        }else if (val1 instanceof long[]){
            val1_size = ((long[])val1).length;
        }else if (val1 instanceof double[]){
            val1_size = ((double[])val1).length;
        }else if (val1 instanceof BigInteger[]){
            val1_size = ((BigInteger[])val1).length;
        }else{
            return ValueAndModified.MISSING_NONSENSICAL;
        }

        if (val2 instanceof String[]){
            val2_size = ((String[])val2).length;
        }else if (val2 instanceof long[]){
            val2_size = ((long[])val2).length;
        }else if (val2 instanceof double[]){
            val2_size = ((double[])val2).length;
        }else if (val2 instanceof BigInteger[]){
            val2_size = ((BigInteger[])val2).length;
        }else{
            return ValueAndModified.MISSING_NONSENSICAL;
        }

        if (val1_size != val2_size){
            return ValueAndModified.MISSING_NONSENSICAL;
        }

        if (val1 instanceof String[] || val1 instanceof long[]){
            if (val2 instanceof double[] || val2 instanceof long[] || val2 instanceof BigInteger[]){
                if (val1_size == 0){
                    return ValueAndModified.MISSING_NONSENSICAL;
                    // if (val2 instanceof BigInteger[]){
                    //     return new ValueAndModified(BigInteger.ZERO, ValueTuple.UNMODIFIED);
                    // }else{
                    //     return new ValueAndModified(0.0, ValueTuple.UNMODIFIED);
                    // }
                }
            
                int index = ArraysPlume.indexOf((Object[])val1, val3);
                if (index==-1){
                    return ValueAndModified.MISSING_NONSENSICAL;
                    // if (val2 instanceof BigInteger[]){
                    //     return new ValueAndModified(BigInteger.ZERO, ValueTuple.UNMODIFIED);
                    // }else{
                    //     return new ValueAndModified(0.0, ValueTuple.UNMODIFIED);
                    // }
                }
                Object val;
               if (val2 instanceof double[]){
                    val = ((double[])val2)[index];
                    val = Intern.intern(val);
                }else if (val2 instanceof long[]){
                    val = ((long[])val2)[index];
                    val = Intern.intern(val);
                }else{
                    val = ((BigInteger[])val2)[index];
                }
                return new ValueAndModified(val, mod);
            }else{
                return ValueAndModified.MISSING_NONSENSICAL;
            }
        }else  if (val1 instanceof BigInteger[]){
            if (val2 instanceof double[] || val2 instanceof long[] || val2 instanceof BigInteger[]){
                if (val1_size == 0){
                    return ValueAndModified.MISSING_NONSENSICAL;
                    // if (val2 instanceof BigInteger[]){
                    //     return new ValueAndModified(BigInteger.ZERO, ValueTuple.UNMODIFIED);
                    // }else{
                    //     return new ValueAndModified(0.0, ValueTuple.UNMODIFIED);
                    // }
                }
            
                int index = -1;
                for (int _index=0; _index<val1_size; _index++){
                    if (((BigInteger[])val1)[_index].equals(val3)){
                        index = _index;
                    }
                }
                if (index==-1){
                    return ValueAndModified.MISSING_NONSENSICAL;
                    // if (val2 instanceof BigInteger[]){
                    //     return new ValueAndModified(BigInteger.ZERO, ValueTuple.UNMODIFIED);
                    // }else{
                    //     return new ValueAndModified(0.0, ValueTuple.UNMODIFIED);
                    // }
                }
                Object val;
                if (val2 instanceof double[]){
                    val = ((double[])val2)[index];
                    val = Intern.intern(val);
                }else if (val2 instanceof long[]){
                    val = ((long[])val2)[index];
                    val = Intern.intern(val);
                }else{
                    val = ((BigInteger[])val2)[index];
                }
                return new ValueAndModified(val, mod);
            }else{
                return ValueAndModified.MISSING_NONSENSICAL;        
            }
        }else{
            return ValueAndModified.MISSING_NONSENSICAL;
        }

        // String[] val1_array = (String[]) val1;
        // for (int i=0; i< val1_array.length; i++){
        //     val1_array[i] = val1_array[i].toLowerCase();
        // }

        // String val3 = base3.getStringValue(full_vt);
        // val3 = val3.toLowerCase();

        // if (val2 instanceof double[]){
        //     double[] val2_array = (double[]) val2;
        //     if (val1_array.length != val2_array.length){
        //         return ValueAndModified.MISSING_NONSENSICAL;
        //     }

        //     int mod =
        //     (((mod1 == ValueTuple.UNMODIFIED)
        //     && (mod2 == ValueTuple.UNMODIFIED)
        //     && (mod3 == ValueTuple.UNMODIFIED))
        //     ? ValueTuple.UNMODIFIED
        //     : ValueTuple.MODIFIED);

        //     if (val1_array.length == 0){
        //         return ValueAndModified.MISSING_NONSENSICAL;
        //     }
            
        //     int index = ArraysPlume.indexOf(val1_array, val3);
        //     if (index==-1){
        //         // double val = 0;
        //         // return new ValueAndModified(val, ValueTuple.UNMODIFIED);
        //         return ValueAndModified.MISSING_NONSENSICAL;
        //     }

        //     double val = val2_array[index];
        //     val = Intern.intern(val);
        //     return new ValueAndModified(val, mod);
        // }else if (val2 instanceof BigInteger[]){
        //     // System.out.println("Bookkeeping Sum for BigInteger");
        //     BigInteger[] val2_array = (BigInteger[]) val2;
        //     if (val1_array.length != val2_array.length){
        //         return ValueAndModified.MISSING_NONSENSICAL;
        //     }

        //     int mod =
        //     (((mod1 == ValueTuple.UNMODIFIED)
        //     && (mod2 == ValueTuple.UNMODIFIED)
        //     && (mod3 == ValueTuple.UNMODIFIED))
        //     ? ValueTuple.UNMODIFIED
        //     : ValueTuple.MODIFIED);

        //     if (val1_array.length == 0){
        //         BigInteger val = BigInteger.ZERO;
        //         return new ValueAndModified(val, ValueTuple.UNMODIFIED);
        //         // return ValueAndModified.MISSING_NONSENSICAL;
        //     }
            
        //     int index = ArraysPlume.indexOf(val1_array, val3);
        //     if (index==-1){
        //         BigInteger val = BigInteger.ZERO;
        //         return new ValueAndModified(val, ValueTuple.UNMODIFIED);
        //         // return ValueAndModified.MISSING_NONSENSICAL;
        //     }

        //     BigInteger val = val2_array[index];
        //     // System.out.println(val);
        //     // val = Intern.intern(val);
        //     return new ValueAndModified(val, mod);
        // }else{
        //     assert(false);
        //     return null;
        // }    
    }

    @Override
    protected VarInfo makeVarInfo() {
        // TODO Auto-generated method stub
        
        return VarInfo.make_subscript(values_var(), key_var(), 0);
    }

    @Override
    public boolean isSameFormula(Derivation other) {
        // TODO Auto-generated method stub
        // return false;
        return (other instanceof InvConUserBookkeeping);
    }

    /** Returns the csharp name. */
    @SideEffectFree
    @Override
    public String csharp_name(String index) {
        String key_name = key_var().csharp_name();
        // We do not need to check if seqvar().isPrestate() because it is redundant.
        return values_var().csharp_name() + ".ValueOf(" + key_name + ")";
    }

    /** Returns the ESC name. */
    @SideEffectFree
    @Override
    public String esc_name(String index) {
        return String.format(
        "%s[%s]",
        values_var().esc_name(), key_var().esc_name());
    }
}
