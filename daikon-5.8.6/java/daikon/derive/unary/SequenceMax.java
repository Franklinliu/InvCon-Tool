package daikon.derive.unary;

import daikon.ValueTuple;
import daikon.VarInfo;
import daikon.derive.Derivation;
import daikon.derive.ValueAndModified;
import org.checkerframework.dataflow.qual.Pure;
import org.checkerframework.dataflow.qual.SideEffectFree;
import org.plumelib.util.ArraysPlume;
import org.plumelib.util.Intern;


import java.math.BigInteger;
// like SequenceMin; if one changes, change the other, too
public final class SequenceMax extends UnaryDerivation {
  // We are Serializable, so we specify a version to allow changes to
  // method signatures without breaking serialization.  If you add or
  // remove fields, you should change this number to the current date.
  static final long serialVersionUID = 20020122L;

  // Variables starting with dkconfig_ should only be set via the
  // daikon.config.Configuration interface.
  /** Boolean. True iff SequencesMax derived variables should be generated. */
  public static boolean dkconfig_enabled = false;

  public SequenceMax(VarInfo vi) {
    super(vi);
  }

  @Override
  public ValueAndModified computeValueAndModifiedImpl(ValueTuple vt) {
    int source_mod = base.getModified(vt);
    if (source_mod == ValueTuple.MISSING_NONSENSICAL) {
      return ValueAndModified.MISSING_NONSENSICAL;
    }
    Object val = base.getValue(vt);
    if (val == null) {
      return ValueAndModified.MISSING_NONSENSICAL;
    }
    if (val instanceof long[]) {
      long[] val_array = (long[]) val;
      if (val_array.length == 0) {
        return ValueAndModified.MISSING_NONSENSICAL;
      }
      return new ValueAndModified(Intern.internedLong(ArraysPlume.max(val_array)), source_mod);
    } else if (val instanceof double[]) {
      double[] val_array = (double[]) val;
      if (val_array.length == 0) {
        return ValueAndModified.MISSING_NONSENSICAL;
      }
      return new ValueAndModified(Intern.internedDouble(ArraysPlume.max(val_array)), source_mod);
    } else if (val instanceof BigInteger[]) {
      BigInteger[] val_array = (BigInteger[]) val;
      if (val_array.length == 0) {
        return ValueAndModified.MISSING_NONSENSICAL;
      }
      BigInteger max_val = val_array[0];
      for (int i=0; i<val_array.length; i++){
        if (max_val.compareTo(val_array[i])<=0){
          max_val = val_array[i];
        }
      }
      return new ValueAndModified(max_val, source_mod);
    } 
    else {
      return ValueAndModified.MISSING_NONSENSICAL;
    }
  }

  @Override
  protected VarInfo makeVarInfo() {
    return VarInfo.make_scalar_seq_func("max", null, base, 0);
  }

  @Pure
  @Override
  public boolean isSameFormula(Derivation other) {
    return (other instanceof SequenceMax);
  }

  /** Returns the ESC name. */
  @SideEffectFree
  @Override
  public String esc_name(String index) {
    return String.format("max(%s)", base.esc_name());
  }
}
